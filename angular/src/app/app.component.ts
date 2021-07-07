import {Component, OnInit} from '@angular/core';
import {RaspberrypiService} from "./core/raspberrypi.service";
import {SseService} from "./core/sse.service";
import {SseData} from "./model/sse-data";
import {RgbaCommand} from "./model/rgba-command";
import {MqttMessageUtil} from "./util/mqtt-message.util";
import {Device} from "./model/device";
import {FormArray, FormBuilder, FormGroup} from "@angular/forms";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {

  deviceForm: FormGroup;
  allDevice: Device = new Device('All Devices', true, [0, 0, 0]);

  constructor(
    private raspberrypiService: RaspberrypiService,
    private sseService: SseService,
    private fb: FormBuilder
  ) {
    this.deviceForm = this.fb.group({
      devices: this.fb.array([this.fb.control(this.allDevice)])
    });
    console.log('devices');
    this.devices.valueChanges.subscribe(a => console.log(a));
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
      if (sseMessageData.event == 'remove' && index > -1) {
        this.devices.removeAt(index);
      } else {
        if (index === -1) {
          const newDevice = new Device(sseMessageData.id, true, sseMessageData.rgb);
          this.devices.push(this.fb.control(newDevice));
        }
      }
    });
  }

  allDevicesChange() {
    // const mqttMessage = MqttMessageUtil.convertRgbaCommandToMqttMessage(rgbaCommand);
    // this.raspberrypiService.toggleAll(mqttMessage).subscribe();
  }

  deviceChange(device: any) {
    console.log('hey');
    // const mqttMessage = MqttMessageUtil.convertRgbaCommandToMqttMessage(rgbaCommand);
    // this.raspberrypiService.toggleOne(device.id, mqttMessage).subscribe();
  }
}
