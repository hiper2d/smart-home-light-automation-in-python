import {Injectable} from '@angular/core';
import {HttpClient, HttpParams} from "@angular/common/http";
import {Observable} from "rxjs";
import {ApiConst} from "../util/api.const";

@Injectable({
  providedIn: 'root'
})
export class RaspberrypiService{

  constructor(private http: HttpClient) { }

  getDevices(): Observable<Array<string>> {
    return this.http.get<Array<string>>(ApiConst.DEVICE);
  }

  toggleOne(deviceId: string, message: string): Observable<any> {
    const params = new HttpParams().set('rgba', message);
    return this.http.get(ApiConst.TOGGLE + '/' + deviceId, {params})
  }

  toggleAll(message: string): Observable<any> {
    const params = new HttpParams().set('rgba', message);
    return this.http.get(ApiConst.TOGGLE, {params})
  }
}
