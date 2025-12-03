import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InetrviewDetailsComponent } from './inetrview-details.component';

describe('InetrviewDetailsComponent', () => {
  let component: InetrviewDetailsComponent;
  let fixture: ComponentFixture<InetrviewDetailsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [InetrviewDetailsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(InetrviewDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
