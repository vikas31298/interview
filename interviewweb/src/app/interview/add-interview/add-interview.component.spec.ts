import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddInterviewComponent } from './add-interview.component';

describe('AddInterviewComponent', () => {
  let component: AddInterviewComponent;
  let fixture: ComponentFixture<AddInterviewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [AddInterviewComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AddInterviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
