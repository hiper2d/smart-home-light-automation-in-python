import {Component, EventEmitter, Input, Output} from '@angular/core';
import {ColorEvent} from "ngx-color/color-wrap.component";
import {ColorSwitcher, RgbaCommand} from "../model/rgba-command";
import {RGBA} from "ngx-color/helpers/color.interfaces";
import {Device} from "../model/device";

@Component({
  selector: 'app-device',
  templateUrl: './device.component.html',
  styleUrls: ['./device.component.scss']
})
export class DeviceComponent {

  static readonly WHITE = new RgbaCommand({on: true}, {r: 255, g: 255, b: 255, a: 1})
  static readonly OFF = new RgbaCommand({on: false}, {r: 0, g: 0, b: 0, a: 0})

  @Input() device?: Device;
  @Output('rgbaChange') emitter = new EventEmitter<RgbaCommand>();
  customColorSwitcher: ColorSwitcher = {on: false};
  customColor: RGBA = {r: 255, g: 255, b: 255, a: 1};
  customColorHex: string = '#fff';
  rgbaCommand: RgbaCommand = new RgbaCommand(this.customColorSwitcher, this.customColor);

  modeChange(value: string) {
    switch (value) {
      case 'custom':
        this.customColorSwitcher.on = true;
        this.emitter.emit(this.rgbaCommand);
        break;
      case 'off':
        this.customColorSwitcher.on = false;
        this.emitter.emit(DeviceComponent.OFF);
        break;
      case 'white':
        this.customColorSwitcher.on = false;
        this.emitter.emit(DeviceComponent.WHITE);
        break;
    }
  }

  rgbChanged(colorEvent: ColorEvent) {
    this.customColor.r = colorEvent.color.rgb.r;
    this.customColor.g = colorEvent.color.rgb.g;
    this.customColor.b = colorEvent.color.rgb.b;
    this.customColorHex = colorEvent.color.hex;
    this.emitter.emit(this.rgbaCommand);
  }

  alphaChanged(colorEvent: ColorEvent) {
    this.customColor.a = colorEvent.color.rgb.a;
    this.emitter.emit(this.rgbaCommand);
  }
}
