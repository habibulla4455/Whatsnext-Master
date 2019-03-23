import { Component, OnInit } from '@angular/core';
import { MoviesService } from '../movies.service';
import { Router } from '@angular/router';
import Swal from 'sweetalert2'

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  movieName: string;
  movieData: Array<any>;
  noDataError: boolean;
  showLoader: boolean;
  user: Object;

  constructor(private Movies: MoviesService, private router: Router) {
    this.user = JSON.parse(localStorage.getItem('user'));
  }

  ngOnInit() {
    if (!localStorage.getItem('user')) {
      Swal.fire('Oops...', 'Something went wrong!', 'error');
      this.router.navigate(['/login']);
    }
  }

  getMoviesByName() {
    this.noDataError = false;
    if (this.movieName != "undefined" && this.movieName != null) {
      this.showLoader = true;
      let dataAvail = document.getElementById("nodata");
      dataAvail.style.display = "none";
      this.Movies.getMovies(this.movieName).subscribe(res => {
        if (res['Search']) {
          this.movieData = res['Search'];
          this.showLoader = false;
        } else if (res['Error'] && !res['Search']) {
          this.showLoader = false;
          this.noDataError = true;
        }
      });
    }
  }

}
