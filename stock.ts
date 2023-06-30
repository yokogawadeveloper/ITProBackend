import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/services/api.service';
import { NgToastService } from 'ng-angular-popup';
import { FormBuilder, FormGroup, FormControl, FormArray, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AlertController } from '@ionic/angular';
import { OverlayEventDetail } from '@ionic/core/components';


@Component({
    selector: 'app-stockmanagementform',
    templateUrl: './stockmanagementform.component.html',
    styleUrls: ['./stockmanagementform.component.scss'],
})



export class StockmanagementformComponent implements OnInit {
    myForm!: FormGroup;
    formSubmitted: boolean = false;
    departmentDropdown: any[] = [];
    categoryDropdown: any[] = [];
    itemDropdown: any[] = [];
    costCenterdropdown: any[] = [];
    procurementData: any = [];
    attachment !: File;


    constructor(
        private apiService: ApiService,
        private toast: NgToastService,
        private formBuilder: FormBuilder,
        private alertController: AlertController,
        private router: Router
    ) { }

    ngOnInit(): void {
        this.myForm = this.formBuilder.group({
            requestType: 'New Hire',
            name: ['', Validators.required],
            department: ['', Validators.required],
            isExpenditure: ['', Validators.required],
            totalBudget: [''],
            utilizedBudget: [''],
            remarks: [''],
            rows: this.formBuilder.array([]),
            additionalAttachments: this.formBuilder.array([]),
        });
        this.addRow(); // Add one row by default

        // Get department dropdown values
        this.apiService.getDepartmentDropdownData().subscribe((res: any) => {
            this.departmentDropdown = res;
        });

        // Get category dropdown values
        this.apiService.getCategoryDropdownData().subscribe((res: any) => {
            this.categoryDropdown = res;
        }
        );

        // Get item dropdown values
        this.apiService.getItemDropdownData().subscribe((res: any) => {
            this.itemDropdown = res;
        }
        );

        // Get cost center dropdown values
        this.apiService.getCostCenterDropdownData().subscribe((res: any) => {
            this.costCenterdropdown = res;
        }
        );

    }//end of ngOnInit

    get rows() {
        return this.myForm.get('rows') as FormArray;
    }

    addRow() {
        const newRow = this.formBuilder.group({
            category: ['', Validators.required],
            item: ['', Validators.required],
            costCenter: ['', Validators.required],
            quantity: ['1', Validators.required],
        });
        this.rows.push(newRow);
    }

    deleteRow(index: number) {
        if (this.rows.length == 1) {
            this.toast.error({
                detail: 'Atleast one row is required',
                position: 'bottom-right',
                duration: 3000,
                type: 'danger'
            })
        } else {
            this.rows.removeAt(index);
        }

    }

    //get file list with name and title
    get additionalAttachments(): FormArray {
        return this.myForm.get('additionalAttachments') as FormArray;
    }

    addAttachmentField(): void {
        const attachmentFormGroup = this.formBuilder.group({
            attachments: ['']
        });
        this.additionalAttachments.push(attachmentFormGroup);
    }

    OnAttachmnetUpload($event: any) {
        const file = $event.target.files[0];
        for (let i = 0; i < this.additionalAttachments.length; i++) {
            if (this.additionalAttachments.controls[i].value.attachments == '') {
                this.additionalAttachments.controls[i].patchValue({
                    attachments: file
                });
                break;
            }
        }
    }


    removeAttachmentField(index: number): void {
        this.additionalAttachments.removeAt(index);
    }
    // Getters for form controls
    async presentAlert() {
        const alert = await this.alertController.create({
            header: 'Confirm Submission',
            message: 'Are you sure you want to submit the form?',
            buttons: [
                {
                    text: 'Cancel',
                    role: 'cancel',
                    cssClass: 'secondary',
                    handler: () => {
                        console.log('Confirmation canceled');
                    }
                },
                {
                    text: 'Submit',
                    handler: () => {
                        console.log('Submitting the form...');
                        this.submitForm();
                    }
                }
            ]
        });
        await alert.present();
    }



    submitForm() {
        // console.log(this.myForm.value);
        this.formSubmitted = true;
        if (this.myForm.valid) {
            const formattedData = {
                RequestType: this.myForm.value.requestType,
                Name: this.myForm.value.name,
                Department: this.myForm.value.department,
                IsExpenditure: this.myForm.value.isExpenditure,
                TotalBudget: this.myForm.value.totalBudget,
                UtilizedBudget: this.myForm.value.utilizedBudget,
                Remarks: this.myForm.value.remarks,
                inlineitem: this.myForm.value.rows.map((row: any) => ({
                    category: row.category,
                    item: row.item,
                    costcenter: row.costCenter,
                    quantity: row.quantity,
                })),
                additionalAttachments: this.myForm.value.additionalAttachments.map((attachment: any) => ({
                    attachments: attachment.attachments,
                })),
            };
            this.apiService.postMasterProcurementData(formattedData).subscribe((res: any) => {
                if (res) {
                    const formData = new FormData();
                    for (let i = 0; i < this.myForm.value.additionalAttachments.length; i++) {
                        formData.append('attachment', this.myForm.value.additionalAttachments[i].attachments);
                    }
                    formData.append('procurement_id', res.id);


                    this.apiService.postAttachment(formData).subscribe((res: any) => {
                        if (res) {
                            this.toast.success({
                                detail: 'Form submitted successfully',
                                position: 'bottom-right',
                                duration: 3000,
                                type: 'success'
                            });
                            this.router.navigate(['/dashboard']);
                        }
                    },
                        (err: any) => {
                            this.toast.error({
                                detail: 'OOPS !Something went wrong',
                                position: 'bottom-right',
                                duration: 3000,
                                type: 'danger'
                            })
                        }
                    );
                }
            });
            console.log(this.myForm.value);


        } else {
            this.toast.error({
                detail: 'OOPS !Something went wrong',
                position: 'bottom-right',
                duration: 3000,
                type: 'danger'
            })
        }
    } //end of submitForm

}