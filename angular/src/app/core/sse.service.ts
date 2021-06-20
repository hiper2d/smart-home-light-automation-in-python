import {Injectable, NgZone} from '@angular/core';
import {ApiConst} from "../util/api.const";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class SseService {

  constructor(private zone: NgZone) { }

  getServerSentEvent(): Observable<MessageEvent> {
    return new Observable(observer => {
      const eventSource = new EventSource(ApiConst.LISTEN);
      eventSource.onmessage = event => {
        this.zone.run(() => observer.next(event))
      }
      eventSource.onerror = error => {
        this.zone.run(() => observer.error(error))
      }
    });
  }
}
