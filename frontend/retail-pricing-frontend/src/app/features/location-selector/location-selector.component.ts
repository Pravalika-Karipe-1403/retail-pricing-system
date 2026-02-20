import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatDialogRef } from '@angular/material/dialog';
import { FormsModule } from '@angular/forms';
import { MatSelectModule } from '@angular/material/select';
import { MatButtonModule } from '@angular/material/button';
import { LocationContextService } from '../../core/location-context.service';
import { Observable } from 'rxjs';
import { HttpClient, HttpParams } from '@angular/common/http';
import { EndPointConfig } from '../../helper/endpoint.config';

@Component({
  selector: 'app-location-selector',
  standalone: true,
  imports: [CommonModule, FormsModule, MatSelectModule, MatButtonModule],
  templateUrl: './location-selector.component.html',
  styleUrl: './location-selector.component.scss',
})
export class LocationSelectorComponent implements OnInit {
  selectedCountry: number = 0;
  selectedCity: number = 0;
  selectedStore: number = 0;
  countryList: any;
  cityList: any;
  storeList: any;
  selectedCountryName: string = '';
  selectedCityName: string = '';
  selectedStoreName: string = '';
  baseURL: string = 'http://127.0.0.1:8000/api/';

  constructor(
    private locationService: LocationContextService,
    private http: HttpClient,
    private dialogRef: MatDialogRef<LocationSelectorComponent>
  ) {}

  async ngOnInit() {
    (await this.locationService.GetCountryList()).subscribe({
      next: (data) => {
        this.countryList = data;
      },

      error: (err) => {
        console.error('Error loading country list data', err);
      },
    });
  }

  GetCityList() {
    this.selectedCity = 0;
    this.selectedStore = 0;
    const params = new HttpParams().set('countryId', this.selectedCountry);
    this.http.get(this.baseURL + EndPointConfig.GetCity, { params }).subscribe({
      next: (data) => {
        this.cityList = data || [];
      },
      error: (err) => {
        console.error('Error loading city list', err);
      },
    });
  }

  GetStoreList() {
    this.selectedStore = 0;
    const params = new HttpParams().set('cityId', this.selectedCity);
    this.http
      .get(this.baseURL + EndPointConfig.GetStore, { params })
      .subscribe({
        next: (data) => {
          this.storeList = data || [];
        },
        error: (err) => {
          console.error('Error loading store list', err);
        },
      });
  }

  apply() {
    const location = {
      country: this.selectedCountryName,
      city: this.selectedCityName,
      storeId: this.selectedStoreName,
    };

    // save in context service (optional but good)
    this.locationService.setLocation(location);

    // RETURN DATA TO CALLER
    this.dialogRef.close(location);
  }
}
