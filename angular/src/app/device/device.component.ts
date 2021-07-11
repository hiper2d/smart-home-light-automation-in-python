import {Component, EventEmitter, forwardRef, OnInit, Output} from '@angular/core';
import {ColorEvent} from "ngx-color/color-wrap.component";
import {ColorSwitcher, RgbaCommand} from "../model/rgba-command";
import {RGBA} from "ngx-color/helpers/color.interfaces";
import {Device} from "../model/device";
import {RgbUtil} from "../util/rgb.util";
import {ControlValueAccessor, NG_VALUE_ACCESSOR} from "@angular/forms";

@Component({
  selector: 'app-device',
  templateUrl: './device.component.html',
  styleUrls: ['./device.component.scss'],
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => DeviceComponent),
      multi: true
    }
  ]
})
export class DeviceComponent implements OnInit, ControlValueAccessor {

  static readonly WHITE = {r: 255, g: 255, b: 255, a: 1}
  static readonly OFF = {r: 0, g: 0, b: 0, a: 0}

  device: Device | undefined;
  customColorSwitcher: ColorSwitcher = {on: false};
  customColor: RGBA = {r: 255, g: 255, b: 255, a: 1};
  customColorDirty = false;
  customColorHex: string = '#fff';

  ngOnInit(): void {
  }

  registerOnChange(fn: any): void {
    this.onChange = fn;
  }

  registerOnTouched(fn: any): void {
  }

  setDisabledState(isDisabled: boolean): void {
  }

  writeValue(obj: Device): void {
    this.device = obj;
    const [r, g, b] = obj.rgb;
    this.customColor = RgbUtil.convertRgbArrayIntoRgba([r, g, b]);
  }

  modeChange(value: string) {
    switch (value) {
      case 'custom':
        this.customColorSwitcher.on = true;
        if (this.customColorDirty) {
          this.device!.rgb = RgbUtil.convertRgbToRgbArray(this.customColor);
          this.onChange(this.device!);
        }
        break;
      case 'off':
        this.customColorSwitcher.on = false;
        this.device!.rgb = RgbUtil.convertRgbToRgbArray(this.customColor);
        this.onChange(this.device!);
        break;
      case 'white':
        this.customColorSwitcher.on = true;
        this.device!.on = true;
        this.customColor = DeviceComponent.WHITE;
        this.onChange(this.device!);
        break;
    }
  }

  rgbChanged(colorEvent: ColorEvent) {
    this.customColor.r = colorEvent.color.rgb.r;
    this.customColor.g = colorEvent.color.rgb.g;
    this.customColor.b = colorEvent.color.rgb.b;
    this.customColorHex = colorEvent.color.hex;
    this.device!.rgb = RgbUtil.convertRgbToRgbArray(this.customColor);
    this.customColorDirty = true;
    this.onChange(this.device!);
  }

  alphaChanged(colorEvent: ColorEvent) {
    this.customColor.a = colorEvent.color.rgb.a;
    this.device!.rgb = RgbUtil.convertRgbToRgbArray(this.customColor);
    this.customColorDirty = true;
    this.onChange(this.device!);
  }

  private onChange(device: Device) {
  }
}
