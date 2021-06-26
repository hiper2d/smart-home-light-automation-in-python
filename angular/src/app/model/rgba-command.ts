import {RGB} from "ngx-color/helpers/color.interfaces";

export interface Alpha {
  value: number;
}

export class RgbaCommand {
  constructor(public on: boolean, public rgb: RGB, public a: Alpha) {
  }
}
