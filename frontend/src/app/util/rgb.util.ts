import {RGBA} from "ngx-color/helpers/color.interfaces";



export class RgbUtil {

  static convertRgbaToArray(rgba: RGBA): Array<number> {
    return [rgba.r, rgba.g, rgba.b, rgba.a];
  }

  static convertArrayToRgba([r, g, b, a]: Array<number>): RGBA {
    return {r: r, g: g, b: b, a: a };
  }

  static rgbArrayToString([r, g, b, a]: Array<number>): string {
    return `${r},${g},${b},${a}`
  }

  static rgbToHex(rgba: RGBA) {
    return "#" + this.numberToHex(rgba.r) + this.numberToHex(rgba.g) + this.numberToHex(rgba.b);
  }

  private static numberToHex(c: number) {
    var hex = c.toString(16);
    return hex.length == 1 ? "0" + hex : hex;
  }
}
