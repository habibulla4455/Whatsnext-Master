import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class MoviesService {
  moviesResponse: any;
  detailResponse: any;

  constructor(private http: HttpClient) { }

  /**
   * set heades here
   */
  public setHeader() {
    return new HttpHeaders({
      "Content-Type": 'application/json',
      "Accept": 'application/json'
    })
  }

  getMovies(name) {
    let url = `http://www.omdbapi.com/?s=${name}&apikey=`;
    return this.http.get(url);
  }

  getMovieDetail(name) {
    let url = `http://www.omdbapi.com/?t=${name}&apikey=`;
    return this.http.get(url);
  }

  getUsers() {
    return this.http.get('https://whatnext-d6110.firebaseio.com/signup.json');
  }

  getRecommendation(name) {
    return this.http.post("http://localhost:5000/api/v1/movies", { 'title': name });
  }

}
