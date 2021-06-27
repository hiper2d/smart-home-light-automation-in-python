import {RGBA} from "ngx-color/helpers/color.interfaces";

export class Device {
  constructor(
    public id: string,
    mac?: string,
    on: boolean = false,
    rgba?: RGBA
  ) {
  }
}
