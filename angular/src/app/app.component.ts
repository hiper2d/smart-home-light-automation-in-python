import {Component, OnInit} from '@angular/core';
import {RaspberrypiService} from "./core/raspberrypi.service";
import {SseService} from "./core/sse.service";
import {SseData} from "./model/sse-data";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {

  devices: Array<string> = [];

  constructor(private raspberrypiService: RaspberrypiService, private sseService: SseService) {

  }

  ngOnInit(): void {
    this.loadDevices();
  }

  loadDevices() {
    this.raspberrypiService.getDevices().subscribe(listOfDevices => this.devices = listOfDevices);
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

  everythingOn() {
    this.raspberrypiService.everythingToggle('on').subscribe();
  }

  everythingOff() {
    this.raspberrypiService.everythingToggle('off').subscribe();
  }

  hitDevice(device: string) {
    console.log('Clicked at ' + device)
  }
}
