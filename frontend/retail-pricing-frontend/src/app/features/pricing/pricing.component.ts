import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { Pricing, PricingService } from './pricing.service';
import { MatDialog } from '@angular/material/dialog';
import { LocationSelectorComponent } from '../location-selector/location-selector.component';
import { MatPaginatorModule, PageEvent } from '@angular/material/paginator';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { MatFormFieldModule } from '@angular/material/form-field';
import { debounceTime, distinctUntilChanged } from 'rxjs/operators';
import { Subject } from 'rxjs';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { PricingHistoryDialogComponent } from '../pricing-history-dialog/pricing-history-dialog.component';

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
    MatPaginatorModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatFormFieldModule,
    MatProgressSpinnerModule,
  ],

  templateUrl: './pricing.component.html',
  styleUrls: ['./pricing.component.scss'],
})
export class PricingComponent implements OnInit {
  // Table columns
  columns: string[] = [
    'sku',
    'productName',
    'price',
    'effectiveDate',
    'action',
  ];

  // Table data
  dataSource = new MatTableDataSource<Pricing>([]);

  // Backup data for filtering
  allData: any[] = [];

  // Free text filter
  filter: string = '';
  totalRecords = 0;
  pageSize = 50;
  pageIndex = 1;
  selectedLocation: any;
  editingCell: any = {
    rowId: null,
    field: null,
  };

  editedRows = new Set<number>();
  private filterSubject = new Subject<string>();
  isLoading: boolean = false;
  todayDate = new Date();

  constructor(
    private pricingService: PricingService,
    private dialog: MatDialog
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
        this.filterSubject
          .pipe(
            debounceTime(400),

            distinctUntilChanged()
          )
          .subscribe((value) => {
            this.loadData();
          });

        this.loadData();
      }
    });
  }

  loadData() {
    this.isLoading = true;
    this.pricingService
      .getPricing(
        this.pageIndex,
        this.pageSize,
        this.selectedLocation.storeId,
        this.filter
      )

      .subscribe({
        next: (data) => {
          this.dataSource.data = data.rows;
          this.totalRecords = data.total;
          this.isLoading = false;
        },

        error: (err) => {
          this.isLoading = false;
          console.error('Error loading pricing data', err);
        },
      });
  }

  // Free text filter for Product / SKU
  applyFilter(value: string): void {
    this.pageIndex = 1;
    this.filterSubject.next(value);
  }

  startEdit(rowId: number, field: string) {
    this.editingCell = {
      rowId,
      field,
    };
  }

  isEditing(rowId: number, field: string) {
    return this.editingCell.rowId === rowId && this.editingCell.field === field;
  }

  stopEdit(row: any) {
    this.editedRows.add(row.pricing_id);

    this.editingCell = {
      rowId: null,
      field: null,
    };
  }

  saveAll(): void {
    const updatedRows = this.dataSource.data
      .filter((row: Pricing) => this.editedRows.has(row.pricing_id))
      .map((row: Pricing) => ({
        id: row.pricing_id,
        product_id: row.product_id,
        store_id: row.store_id,
        price: row.price,
        effective_date: row.effective_date,
        is_active: row.is_active,
      }));

    if (updatedRows.length === 0) {
      alert('No changes to save');
      return;
    }

    this.pricingService.bulkUpdatePricing(updatedRows).subscribe({
      next: () => {
        alert('All changes saved successfully');
        this.editedRows.clear();
      },

      error: () => {
        alert('Error saving changes');
      },
    });
  }

  // Upload button
  upload(): void {
    alert(`Upload pricing for Store: ${this.selectedLocation?.store}`);
  }

  pageChanged(event: PageEvent) {
    this.pageIndex = event.pageIndex + 1;
    this.pageSize = event.pageSize;
    this.loadData();
  }

  changeLocation() {
    this.openLocationPopup();
  }

  priceHistoryDetails(row: Pricing) {
    this.pricingService.GetHistory(row.product_id, row.store_id).subscribe((data) => {
      this.dialog.open(PricingHistoryDialogComponent, {
        width: '600px',
        data: data.rows,
      });
    });
  }
}
