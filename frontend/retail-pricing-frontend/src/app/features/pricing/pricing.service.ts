import { Injectable } from '@angular/core';

import { of } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class PricingService {
  data = [
    {
      sku: 'SKU001',

      productName: 'iPhone',

      price: 50000,
    },

    {
      sku: 'SKU002',

      productName: 'Samsung',

      price: 40000,
    },

    {
      sku: 'SKU003',

      productName: 'Pixel',

      price: 45000,
    },

    {
      sku: 'SKU004',

      productName: 'Nokia',

      price: 20000,
    },
  ];

  getPricing(page: number, pageSize: number, filter: string) {
    let filtered = this.data;

    if (filter) {
      filtered = filtered.filter(
        (x) =>
          x.productName.toLowerCase().includes(filter.toLowerCase()) ||
          x.sku.toLowerCase().includes(filter.toLowerCase())
      );
    }

    const start = page * pageSize;

    const end = start + pageSize;

    return of({
      rows: filtered.slice(start, end),

      totalCount: filtered.length,
    });
  }

  updatePrice(row: any) {
    return of(true);
  }
}
