import {RGB, RGBA} from "ngx-color/helpers/color.interfaces";

export interface ColorSwitcher {
  on: boolean;
}

export class RgbaCommand {

  constructor(public on: ColorSwitcher, public rgba: RGBA) {
  }
}
