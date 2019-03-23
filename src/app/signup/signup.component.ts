import { Component, OnInit, ViewChild } from '@angular/core';
import { User } from '../user.model';
import { NgForm } from '@angular/forms';
import { Router } from '@angular/router';
import * as firebase from 'firebase';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit {
  @ViewChild('f') userForm: NgForm;
  cpass: string;
  user: User = new User();
  loggedIn: boolean;

  constructor(private router: Router) { }

  ngOnInit() {
    if (localStorage.getItem('user')) {
      this.router.navigate(['/home']);
    }
  }

  signup(userForm) {
    if (this.userForm.valid) {
      this.loggedIn = true;
      firebase.database().ref('signup/').push(this.user).then(res => {
        this.loggedIn = true;
        localStorage.setItem('user', JSON.stringify({ ...this.user, userid: res.key }));
        localStorage.setItem('loggedIn', this.loggedIn.toString());
        this.router.navigate(['/home']);
      });
    }
  }

}
