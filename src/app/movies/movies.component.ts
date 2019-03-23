import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MoviesService } from '../movies.service';
import * as firebase from 'firebase';
import Swal from 'sweetalert2'

@Component({
  selector: 'app-movies',
  templateUrl: './movies.component.html',
  styleUrls: ['./movies.component.css']
})
export class MoviesComponent implements OnInit {
  user: Object; 
  movieData: Object;
  currentData;
  showLoader:boolean;

  constructor(private Movies: MoviesService, private activatedRoute: ActivatedRoute, private router: Router) {
    this.user = JSON.parse(localStorage.getItem('user'));
  }

  ngOnInit() {
    this.showLoader = true;
    if (!localStorage.getItem('user')) {
      Swal.fire('Oops...', "You're not logged in!", 'error');
      this.router.navigate(['/login']);
    }
    this.activatedRoute.params.subscribe(params => {
      this.Movies.getMovieDetail(params.name).subscribe(res => {
        this.movieData = res;
        this.showLoader = false;
      }); 
    });
  }

  submitRating(rateIndex){
    rateIndex = this.currentData;
    firebase.database().ref('movierating/').push({userId: this.user['userid'], userRating: rateIndex, movieName: this.movieData['Title']});
  }   
}
