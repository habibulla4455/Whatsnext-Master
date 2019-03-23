import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MoviesService } from '../movies.service';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-recom',
  templateUrl: './recom.component.html',
  styleUrls: ['./recom.component.css']
})
export class RecomComponent implements OnInit {

  user: Object;
  recomMovies = [];
  noDataError: boolean;
  showLoader: boolean;

  constructor(private Movies: MoviesService, private router:Router, private activatedRoute:ActivatedRoute) {
    this.user = JSON.parse(localStorage.getItem('user'));
  }

  ngOnInit() {
    this.showLoader = true;
    if (!localStorage.getItem('user')) {
      Swal.fire('Oops...', "You're not logged in!", 'error');
      this.router.navigate(['/login']);
    }
    this.activatedRoute.params.subscribe(params => {
      this.Movies.getRecommendation(params.name).subscribe(res => {
        if(!res){
          this.noDataError = true;
        }else{
          for(let key in res['Correlation']){
            this.Movies.getMovieDetail(key.substring(0, key.length - 6)).subscribe(res => {
              if(res['Error']){
                console.log(res['Error']);
              }else{
                this.recomMovies.push(res);
              }
              this.showLoader = false;
            });
          }
        } 
      });
    });
  }

}
