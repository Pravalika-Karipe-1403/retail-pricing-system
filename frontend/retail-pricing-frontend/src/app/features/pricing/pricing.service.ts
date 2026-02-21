import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';

import { of } from 'rxjs';
import { EndPointConfig } from '../../helper/endpoint.config';

export interface PricingResponse {
  total: number;
  rows: Pricing[];
}

export interface Pricing {
  pricing_id: number;
  product_id: number;
  store_id: number;
  sku: string;
  product_name: string;
  price: number;
  effective_date: string;
  is_active: boolean
}

@Injectable({ providedIn: 'root' })
export class PricingService {
  baseURL: string = 'http://127.0.0.1:8000/api/';

  constructor(private http: HttpClient) {}

  getPricing(page: number, pageSize: number, storeId: number, filter: string) {
    const params = new HttpParams({
      fromObject: {
        page: page,
        page_size: pageSize,
        store_id: storeId,
        product: filter || '',
      },
    });
    return this.http.get<PricingResponse>(
      this.baseURL + EndPointConfig.GetPricingDetails,
      { params }
    );
  }

  bulkUpdatePricing(request: any[]) {
    return this.http.put(this.baseURL + EndPointConfig.SaveBulkUpdate,
      { items: request }
    );
  }

  GetHistory(productId: number, storeId: number) {
    const params = new HttpParams({
      fromObject: {
        product_id: productId,
        store_id: storeId
      },
    });
    return this.http.get<PricingResponse>(this.baseURL + EndPointConfig.GetPricingHistory,
      { params }
      )
  }
}
