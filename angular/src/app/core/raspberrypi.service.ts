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

  saveDevice(device: Device): Observable<Device> {
    return this.http.put<Device>(ApiConst.DEVICE, device);
  }

  toggleAll(rgba: Array<number>): Observable<any> {
    const params = new HttpParams().set('rgba', RgbUtil.rgbArrayToString(rgba));
    return this.http.get(ApiConst.TOGGLE, {params})
  }
}
