import { Routes } from '@angular/router';
import { RetailListComponent } from './features/retail-list/retail-list.component';

export const routes: Routes = [
    { path: '', pathMatch: 'full', redirectTo: 'retail-list' },
    { path: 'retail-list', component: RetailListComponent }
];
