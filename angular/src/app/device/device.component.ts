import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {ColorEvent} from "ngx-color/color-wrap.component";
import {RGB, RGBA} from "ngx-color/helpers/color.interfaces";
import {Alpha, RgbaCommand} from "../model/rgba-command";

@Component({
  selector: 'app-device',
  templateUrl: './device.component.html',
  styleUrls: ['./device.component.scss']
})
export class DeviceComponent implements OnInit {

  @Input() device?: string;
  @Output('rgbaChange') emitter = new EventEmitter<RgbaCommand>();
  on = false;
  a: Alpha = {value: 1};
  rgb: RGB = {r: 255, g: 255, b: 255};
  rgbaCommand: RgbaCommand = new RgbaCommand(this.on, this.rgb, this.a);

  constructor() { }

  ngOnInit(): void {
  }

  rgbaChange() {
    this.rgbaCommand.on = this.on;
    this.emitter.emit(this.rgbaCommand);
  }

  rgbChanged(colorEvent: ColorEvent) {
    this.rgb.r = colorEvent.color.rgb.r;
    this.rgb.g = colorEvent.color.rgb.g;
    this.rgb.b = colorEvent.color.rgb.b;
    this.emitter.emit(this.rgbaCommand);
  }

  alphaChanged(colorEvent: ColorEvent) {
    this.a.value = colorEvent.color.rgb.a;
    this.emitter.emit(this.rgbaCommand);
  }
}
