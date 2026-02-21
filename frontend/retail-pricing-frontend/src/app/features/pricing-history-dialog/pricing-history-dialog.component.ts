import { Component, Inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MAT_DIALOG_DATA, MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatTableModule } from '@angular/material/table';

@Component({
  selector: 'app-pricing-history-dialog',
  standalone: true,
  imports: [CommonModule, MatDialogModule, MatButtonModule, MatTableModule],
  templateUrl: './pricing-history-dialog.component.html',
  styleUrls: ['./pricing-history-dialog.component.scss'],
})

export class PricingHistoryDialogComponent {
  columns: string[] = ['price', 'effective_date', 'updated_at'];
  constructor(@Inject(MAT_DIALOG_DATA) public data: any) {}
}
