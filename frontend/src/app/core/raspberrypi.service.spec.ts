import { TestBed } from '@angular/core/testing';

import { RaspberrypiService } from './raspberrypi.service';

describe('RaspberrypiService', () => {
  let service: RaspberrypiService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(RaspberrypiService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
