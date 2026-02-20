import { Component, OnInit } from '@angular/core';

import { CommonModule } from '@angular/common';

import { FormsModule } from '@angular/forms';

import { MatTableModule } from '@angular/material/table';

import { MatInputModule } from '@angular/material/input';

import { MatButtonModule } from '@angular/material/button';

import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';

import { PricingService } from './pricing.service';
import { LocationContextService } from '../../core/location-context.service';
import { MatDialog } from '@angular/material/dialog';
import { LocationSelectorComponent } from '../location-selector/location-selector.component';
import { MatPaginatorModule, PageEvent } from '@angular/material/paginator';


@Component({
  selector: 'app-pricing',

  standalone: true,

  imports: [
    CommonModule,
    FormsModule,
    MatTableModule,
    MatInputModule,
    MatButtonModule,
    MatCardModule,
    MatIconModule,
    MatPaginatorModule
  ],

  templateUrl: './pricing.component.html',
  styleUrls: ['./pricing.component.scss'],
})
export class PricingComponent implements OnInit {
  // Table columns
  columns: string[] = ['sku', 'productName', 'price', 'action'];

  // Table data
  dataSource: any[] = [];

  // Backup data for filtering
  allData: any[] = [];

  // Free text filter
  filter: string = '';
  totalRecords = 0;
  pageSize = 50;
  pageIndex = 0;
  selectedLocation: any;

  constructor(
    private pricingService: PricingService,
    private dialog: MatDialog,
    private locationService: LocationContextService
  ) {}

  ngOnInit(): void {
    this.openLocationPopup();
  }

  openLocationPopup() {
    const dialogRef = this.dialog.open(LocationSelectorComponent, {
      width: '500px',
      height: '450px',
      disableClose: true,
    });

    dialogRef.afterClosed().subscribe((location) => {
      if (location) {
        this.selectedLocation = location;

        this.loadData();
      }
    });
  }

  loadData(): void {
    this.pricingService
      .getPricing(
        this.pageIndex,
        this.pageSize,
        this.filter
      )

      .subscribe({
        next: (data) => {
          this.dataSource = data.rows;
          this.totalRecords = data.totalCount;
        },

        error: (err) => {
          console.error('Error loading pricing data', err);
        },
      });
  }

  // Free text filter for Product / SKU
  applyFilter(): void {
    const searchValue = this.filter.toLowerCase();
    this.dataSource = this.allData.filter(
      (row) =>
        row.productName.toLowerCase().includes(searchValue) ||
        row.sku.toLowerCase().includes(searchValue)
    );
  }

  // Save updated price
  save(row: any): void {
    this.pricingService
      .updatePrice(row)

      .subscribe({
        next: () => {
          alert('Price updated successfully');
        },

        error: () => {
          alert('Error updating price');
        },
      });
  }

  // Upload button
  upload(): void {
    alert(`Upload pricing for Store: ${this.selectedLocation?.store}`);
  }

  pageChanged(event: PageEvent) {
    this.pageIndex = event.pageIndex;
    this.pageSize = event.pageSize;
    this.loadData();
  }
}
