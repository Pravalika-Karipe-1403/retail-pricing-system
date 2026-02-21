import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PricingHistoryDialogComponent } from './pricing-history-dialog.component';

describe('PricingHistoryDialogComponent', () => {
  let component: PricingHistoryDialogComponent;
  let fixture: ComponentFixture<PricingHistoryDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PricingHistoryDialogComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(PricingHistoryDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
