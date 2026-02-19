import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { AgGridAngular } from 'ag-grid-angular';
import { ColDef } from 'ag-grid-community';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatCardModule } from '@angular/material/card';

interface Pricing {
  storeId: number;
  sku: string;
  productName: string;
  price: number;
  date: string;
}

@Component({
  selector: 'app-retail-list',
  standalone: true,
  imports: [
    AgGridAngular,
    CommonModule,
    FormsModule,
    MatSelectModule,
    MatFormFieldModule,
    MatButtonModule,
    MatIconModule,
    MatCardModule
  ],
  templateUrl: './retail-list.component.html',
  styleUrl: './retail-list.component.scss',
})
export class RetailListComponent implements OnInit {
  selectedLocations: string[] = [];
  selectAllValue = 'SELECT_ALL';
  locations: string[] = ['India', 'USA', 'UK', 'Canada', 'Australia'];
  

  columnDefs: ColDef<Pricing>[] = [
    { field: 'storeId' },
    { field: 'sku' },
    { field: 'productName' },
    { field: 'price', editable: true, valueFormatter: this.priceFormatter },
    { field: 'date' },
  ];

  rowData: Pricing[] = [
    {
      storeId: 1,
      sku: 'SKU001',
      productName: 'iPhone',
      price: 50000,
      date: '2026-01-01',
    },
    {
      storeId: 2,
      sku: 'SKU002',
      productName: 'Samsung',
      price: 40000,
      date: '2026-01-01',
    },
  ];

  defaultColDef: ColDef = {
    sortable: true,
    filter: true,
    resizable: true,
    floatingFilter: false,
    suppressMenu: false
  };

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.loadPricingData();
  }

  loadPricingData() {
    this.http.get<any>('http://localhost:8000/pricing').subscribe({
      next: (data) => {
        this.rowData = data;
      },

      error: (err) => {
        console.error('Error loading pricing data', err);
      },
    });
  }

  priceFormatter(params: any) {
    if (params.value != null) {
      return '$' + params.value.toLocaleString();
    }
    return '';
  }

  onSearch() {
    console.log('Search clicked');
    this.loadPricingData();
  }

  onReset() {
    this.selectedLocations = [];
    this.loadPricingData();
  }
}
