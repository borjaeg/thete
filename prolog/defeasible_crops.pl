is_a(c4,c7).
is_a(c4,c3).
is_a(c5,c2).
is_a(c3,c2).
is_a(c6,c).
is_a(c2,c).

permitir(Cultivo, Producto, Plaga):- is_a(Cultivo, CultivoPadre), 
	  \+ not(permitir(Cultivo, Producto, Plaga)),
	  permitir(CultivoPadre, Producto, Plaga).

permitir(c,p,pl).

not(permitir(c3,p,pl)).