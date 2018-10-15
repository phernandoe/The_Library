create table Artist (
 id integer primary key autoincrement,
 name varchar(64) not null,
 genre varchar(64) not null,
 hometown varchar(64) not null,
 description varchar(128) not null
);

create table Venue (
	id integer primary key autoincrement,
  name varchar(64) not null,
	location varchar(64) not null,
	capacity integer not null
);

create table Event (
	id integer primary key autoincrement,
  name varchar(64) not null,
  time datetime,
  venueID integer not null,
 	foreign key (venueID) references Venue(id)
);

create table ArtistToEvent (
	id integer primary key autoincrement,
 	artistID integer not null,
	eventID  integer not null,
	foreign key (artistID) references Artist(id),
	foreign key (eventID) references Event(id)
);

create table User (
	id integer primary key autoincrement,
	username varchar(64) not null,
	email varchar(64) not null,
	password_hash varchar(128) not null
);