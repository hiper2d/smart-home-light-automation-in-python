import {RgbaCommand} from "../model/rgba-command";

const COEFFICIENT = 1023 / 255;

function scale(color: number, brightness: number): number {
  return Math.round(color * COEFFICIENT * brightness);
}

export class MqttMessageUtil {

  static convertRgbaCommandToMqttMessage(command: RgbaCommand): string {
    const r = command.rgba.r;
    const g = command.rgba.g;
    const b = command.rgba.b;
    const a = command.rgba.a;
    return `${scale(r,a)},${scale(g,a)},${scale(b,a)}`;
  }
}
