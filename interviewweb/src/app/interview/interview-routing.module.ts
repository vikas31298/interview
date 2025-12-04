import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { InterviewComponent } from './interview.component';
import { AddInterviewComponent } from './add-interview/add-interview.component';
import { ListInterviewsComponent } from './list-interviews/list-interviews.component';
import { InterviewRoomComponent } from './interview-room/interview-room.component';
import { SearchComponent } from './search/search.component';
import { FrequentComponent } from './frequent/frequent.component';
import { ProductManagementComponent } from './product-management/product-management.component';
import { OyrComponent } from './oyr/oyr.component';
import { ArchitectComponent } from './architect/architect.component';
import { BehavioralComponent } from './behavioral/behavioral.component';

const routes: Routes = [
  {
    path: '', component: InterviewComponent,
    children: [
      { path: 'list', component: ListInterviewsComponent },
      { path: 'add', component: AddInterviewComponent },
      { path: 'room', component: InterviewRoomComponent },
      { path: 'search', component: SearchComponent },
      { path: 'frequent', component: FrequentComponent },
      { path: 'product-management', component: ProductManagementComponent },
      { path: 'oyr', component: OyrComponent },
      { path: 'architect', component: ArchitectComponent },
      { path: 'behavioral', component: BehavioralComponent }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class InterviewRoutingModule { }
