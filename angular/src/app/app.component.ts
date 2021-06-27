import {Component, OnInit} from '@angular/core';
import {RaspberrypiService} from "./core/raspberrypi.service";
import {SseService} from "./core/sse.service";
import {SseData} from "./model/sse-data";
import {RgbaCommand} from "./model/rgba-command";
import {MqttMessageUtil} from "./util/mqtt-message.util";
import {Device} from "./model/device";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {

  allDevice: string = 'All Devices';
  devices: Array<string> = ['sdfsdfdsf', 'asdfsdf'];

  constructor(private raspberrypiService: RaspberrypiService, private sseService: SseService) {
  }

  ngOnInit(): void {
    this.loadDevices();
  }

  loadDevices() {
    //this.raspberrypiService.getDevices().subscribe(listOfDevices => this.devices = listOfDevices);
    this.sseService.getServerSentEvent().subscribe((msg: MessageEvent) => {
      const sseMessageData = JSON.parse(msg.data) as SseData;
      let index = this.devices.indexOf(sseMessageData.id);
      if (sseMessageData.event == 'remove' && index > -1) {
        this.devices.splice(index, 1)
      } else {
        if (index === -1) {
          this.devices.push(sseMessageData.id);
        }
      }
    });
  }

  allDevicesChange(rgbaCommand: RgbaCommand) {
    const mqttMessage = MqttMessageUtil.convertRgbaCommandToMqttMessage(rgbaCommand);
    this.raspberrypiService.toggleAll(mqttMessage).subscribe();
  }

  deviceChange(deviceId: string, rgbaCommand: RgbaCommand) {
    const mqttMessage = MqttMessageUtil.convertRgbaCommandToMqttMessage(rgbaCommand);
    this.raspberrypiService.toggleOne(deviceId, mqttMessage).subscribe();
  }
}
