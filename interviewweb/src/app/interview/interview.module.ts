import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';

import { InterviewRoutingModule } from './interview-routing.module';
import { InterviewComponent } from './interview.component';
import { AddInterviewComponent } from './add-interview/add-interview.component';
import { InterviewRoomComponent } from './interview-room/interview-room.component';
import { ListInterviewsComponent } from './list-interviews/list-interviews.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { SearchComponent } from './search/search.component';
import { InetrviewDetailsComponent } from './inetrview-details/inetrview-details.component';
import { SanitizeHtmlPipe } from './pipes/sanitize-html.pipe';
import { FrequentComponent } from './frequent/frequent.component';
import { ProductManagementComponent } from './product-management/product-management.component';
import { OyrComponent } from './oyr/oyr.component';
import { ArchitectComponent } from './architect/architect.component';
import { MarkdownPipe } from './pipes/markdown.pipe';
import { BehavioralComponent } from './behavioral/behavioral.component';


@NgModule({
  declarations: [
    InterviewComponent,
    AddInterviewComponent,
    InterviewRoomComponent,
    ListInterviewsComponent,
    SearchComponent,
    InetrviewDetailsComponent,
    SanitizeHtmlPipe,
    FrequentComponent,
    ProductManagementComponent,
    OyrComponent,
    ArchitectComponent,


    MarkdownPipe,       // For markdown to HTML conversion
    SanitizeHtmlPipe, BehavioralComponent    // For safe HTML rendering
  ],
  imports: [
    CommonModule,
    InterviewRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule
  ]
})
export class InterviewModule { }
