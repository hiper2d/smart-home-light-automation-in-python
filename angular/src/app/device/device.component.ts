import {Component, EventEmitter, forwardRef, OnInit, Output} from '@angular/core';
import {ColorEvent} from "ngx-color/color-wrap.component";
import {RGBA} from "ngx-color/helpers/color.interfaces";
import {Device} from "../model/device";
import {RgbUtil} from "../util/rgb.util";
import {ControlValueAccessor, NG_VALUE_ACCESSOR} from "@angular/forms";
import {Const} from "../util/const";

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

  @Output('manualChange') deviceEmitter = new EventEmitter<Device>();
  device: Device | undefined;
  mode?: string = 'off';
  customColor: RGBA = {r: 255, g: 255, b: 255, a: 1.0};
  customColorDirty = false;
  customColorHex = Const.WHITE_HEX;

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
    const [r, g, b, a] = obj.rgba;
    this.customColor = RgbUtil.convertArrayToRgba([r, g, b, a]);
    if (this.device!.id === Const.ALL_DEVICES_ID) {
      this.mode = undefined;
      return;
    }
    if (this.device?.on) {
      if(this.customColor.r === 255 && this.customColor.g === 255 && this.customColor.b === 255) {
        this.mode = 'white'
        this.customColorHex = Const.WHITE_HEX;
        this.customColorDirty = false;
      } else {
        this.mode = 'custom';
        this.customColorHex = RgbUtil.rgbToHex(this.customColor);
        this.customColorDirty = true;
      }
    } else {
      this.mode = 'off';
    }
  }

  modeChange(value: string) {
    this.mode = value;
    switch (value) {
      case 'custom':
        this.device!.on = true;
        if (this.customColorDirty) {
          this.device!.rgba = RgbUtil.convertRgbaToArray(this.customColor);
          this.deviceEmitter.emit(this.device);
          this.onChange(this.device!);
        }
        break;
      case 'off':
        this.device!.on = false;
        this.deviceEmitter.emit(this.device);
        this.onChange(this.device!);
        break;
      case 'white':
        this.device!.on = true;
        this.customColor = {...Const.WHITE};
        this.customColorHex = Const.WHITE_HEX;
        this.device!.rgba = RgbUtil.convertRgbaToArray(Const.WHITE);
        this.deviceEmitter.emit(this.device);
        this.onChange(this.device!);
        break;
    }
  }

  rgbChanged(colorEvent: ColorEvent) {
    this.customColor.r = colorEvent.color.rgb.r;
    this.customColor.g = colorEvent.color.rgb.g;
    this.customColor.b = colorEvent.color.rgb.b;
    this.customColorHex = colorEvent.color.hex;
    this.deviceChanged();
  }

  alphaChanged(colorEvent: ColorEvent) {
    this.customColor.a = colorEvent.color.rgb.a;
    this.deviceChanged();
  }

  private deviceChanged() {
    this.device!.rgba = RgbUtil.convertRgbaToArray(this.customColor);
    this.customColor = {...this.customColor};
    this.customColorDirty = true;
    this.onChange(this.device!);
    this.deviceEmitter.emit(this.device);
  }

  private onChange(device: Device) {
  }
}
