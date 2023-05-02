import {Component, OnInit} from '@angular/core';
import {RaspberrypiService} from "./core/raspberrypi.service";
import {SseService} from "./core/sse.service";
import {Device} from "./model/device";
import {FormArray, FormBuilder, FormGroup} from "@angular/forms";
import {Const} from "./util/const";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {

  deviceForm: FormGroup;
  allDevice: Device = new Device(Const.ALL_DEVICES_ID, true, [255, 255, 255, 1]);

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
      const sse_device = JSON.parse(msg.data) as Device;
      let index = this.devices.controls.findIndex(c => c.value.id === sse_device.id);
      switch (sse_device.event) {
        case 'remove':
          if (index > -1) {
            this.devices.removeAt(index);
          }
          break;
        case 'update':
          if (index > -1) {
            let device: Device = this.devices.get('' + index)?.value;
            device.rgba = sse_device.rgba;
            device.on = sse_device.on;
            this.devices.get('' + index)?.patchValue(device);
          }
          break;
        case 'add':
          if (index === -1) {
            this.devices.push(this.fb.control(sse_device));
          }
          break;
      }
    });
  }

  deviceChange(device: Device) {
    if (device.id === Const.ALL_DEVICES_ID) {
      this.raspberrypiService.toggleAll(device.on, device.rgba).subscribe();
    } else {
      this.raspberrypiService.saveDevice(device).subscribe();
    }
  }
}
