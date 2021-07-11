import {RGBA} from "ngx-color/helpers/color.interfaces";

const COEFFICIENT = 1023 / 255;

function scale(color: number, brightness: number): number {
  return Math.round(color * COEFFICIENT * brightness);
}

function scaleBack(color: number): number {
  return Math.round(color / COEFFICIENT);
}

export class RgbUtil {

  static convertRgbToRgbArray(rgba: RGBA): Array<number> {
    const r = scale(rgba.r, rgba.a);
    const g = scale(rgba.g, rgba.a);
    const b = scale(rgba.b, rgba.a);
    return [r, g, b];
  }

  static convertRgbArrayIntoRgba([r, g, b]: Array<number>): RGBA {
    return {r: scaleBack(r), g: scaleBack(g), b: scaleBack(b), a: 1 };
  }

  static rgbArrayToString([r, g, b]: Array<number>): string {
    return `${r},${g},${b}`
  }
}
