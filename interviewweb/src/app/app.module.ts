import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { FrequentComponent } from './interview/frequent/frequent.component';
import { ProductManagementComponent } from './interview/product-management/product-management.component';
import { OyrComponent } from './interview/oyr/oyr.component';
import { ArchitectComponent } from './interview/architect/architect.component';

@NgModule({
  declarations: [
    AppComponent,
    
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
