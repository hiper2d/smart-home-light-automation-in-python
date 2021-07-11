import {Component, OnInit} from '@angular/core';
import {RaspberrypiService} from "./core/raspberrypi.service";
import {SseService} from "./core/sse.service";
import {SseData} from "./model/sse-data";
import {RgbaCommand} from "./model/rgba-command";
import {RgbUtil} from "./util/rgb.util";
import {Device} from "./model/device";
import {FormArray, FormBuilder, FormGroup} from "@angular/forms";

const ALL_DEVICES_ID = 'All Devices'

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {

  deviceForm: FormGroup;
  allDevice: Device = new Device(ALL_DEVICES_ID, true, [0, 0, 0]);

  constructor(
    private raspberrypiService: RaspberrypiService,
    private sseService: SseService,
    private fb: FormBuilder
  ) {
    this.deviceForm = this.fb.group({
      devices: this.fb.array([this.fb.control(this.allDevice)])
    });
  }

  ngOnInit(): void {
    this.loadDevices();
  }

  get devices() {
    return this.deviceForm.get('devices') as FormArray;
  }

  loadDevices() {
    this.raspberrypiService.getDevices().subscribe(listOfDevices => {
      listOfDevices.forEach(d => this.devices.push(this.fb.control(d)));
    });
    this.sseService.getServerSentEvent().subscribe((msg: MessageEvent) => {
      const sseMessageData = JSON.parse(msg.data) as SseData;
      let index = this.devices.controls.findIndex(c => c.value.id === sseMessageData.id);
      switch (sseMessageData.event) {
        case 'remove':
          if (index > -1) {
            this.devices.removeAt(index);
          }
          break;
        case 'update':
          if (index > -1) {
            let device: Device = this.devices.get('' + index)?.value;
            device.rgb = sseMessageData.rgb;
            this.devices.get('' + index)?.patchValue(device);
          }
          break;
        case 'add':
          if (index === -1) {
            const newDevice = new Device(sseMessageData.id, true, sseMessageData.rgb);
            this.devices.push(this.fb.control(newDevice));
          }
          break;
      }
    });
  }

  deviceChange(device: Device) {
    if (device.id === ALL_DEVICES_ID) {
      this.raspberrypiService.toggleAll(device.rgb).subscribe(r => console.log(r));
    } else {
      this.raspberrypiService.saveDevice(device).subscribe(r => console.log(r));
    }
  }
}
