import {RgbaCommand} from "../model/rgba-command";
import {Device} from "../model/device";

export class MqttMessageUtil {

  static readonly OFF = '0,0,0,0';

  static convertRgbaCommandToMqttMessage(command: RgbaCommand): string {
    return command.on
      ? `${command.rgba.r},${command.rgba.g},${command.rgba.b},${command.rgba.a}`
      : MqttMessageUtil.OFF;
  }
}
