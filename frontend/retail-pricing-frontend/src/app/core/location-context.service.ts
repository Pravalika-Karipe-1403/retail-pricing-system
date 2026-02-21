import { HttpClient } from '@angular/common/http';
import { Injectable, signal } from '@angular/core';
import { EndPointConfig } from '../helper/endpoint.config';

export interface LocationContext {
  country: string;
  city: string;
  storeId: number;
  storeName: string;
}

@Injectable({
  providedIn: 'root'
})
export class LocationContextService {

  constructor(private http: HttpClient) {

  }
  private locationSignal = signal<LocationContext | null>(null);
  baseURL: string = 'http://127.0.0.1:8000/api/';

  setLocation(location: LocationContext) {
    this.locationSignal.set(location);
  }

  getLocation() {
    return this.locationSignal();
  }

  clearLocation() {
    this.locationSignal.set(null);
  }

  async GetCountryList(){
    return this.http.get(this.baseURL + EndPointConfig.GetCountry)
  }


}