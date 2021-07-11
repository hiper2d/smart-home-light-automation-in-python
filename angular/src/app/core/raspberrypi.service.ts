import {Injectable} from '@angular/core';
import {HttpClient, HttpParams} from "@angular/common/http";
import {Observable} from "rxjs";
import {ApiConst} from "../util/api.const";
import {Device} from "../model/device";
import {RgbUtil} from "../util/rgb.util";

@Injectable({
  providedIn: 'root'
})
export class RaspberrypiService{

  constructor(private http: HttpClient) { }

  getDevices(): Observable<Array<Device>> {
    return this.http.get<Array<Device>>(ApiConst.DEVICE);
  }

  toggleOne(device: Device): Observable<any> {
    const params = new HttpParams().set('rgb', RgbUtil.rgbArrayToString(device.rgb));
    return this.http.get(ApiConst.TOGGLE + '/' + device.id, {params})
  }

  toggleAll(rgb: Array<number>): Observable<any> {
    const params = new HttpParams().set('rgb', RgbUtil.rgbArrayToString(rgb));
    return this.http.get(ApiConst.TOGGLE, {params})
  }
}
