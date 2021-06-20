import {Component, OnInit} from '@angular/core';
import {RaspberrypiService} from "./core/raspberrypi.service";
import {Observable} from "rxjs";
import {SseService} from "./core/sse.service";

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
      console.log(JSON.parse(msg.data))
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
