1\. La medida de rendimiento (el objetivo)  
Es cómo defines el éxito. Si quieres que un robot limpie rápido, la medida de rendimiento será “minimizar el tiempo”. Si quieres que gaste poca batería, el criterio cambia. Sin un criterio claro, no se puede juzgar si algo es racional.

2\. El conocimiento del medio  
Es lo que el agente sabe del entorno. Si el robot sabe que las alfombras enredan el cepillo, evitará pasar por ellas. Si no lo sabe, no es racional que evite algo que desconoce.

3\. Las acciones disponibles  
Influye en lo que puede hacer. Si el robot puede aspirar, barrer o llamar a ayuda, sus decisiones se eligen de entre ese conjunto. No puedes exigirle una acción que no tiene disponible.

4\. La secuencia de percepciones  
Es el historial: lo que ha visto hasta ahora. Si el robot detecta que hoy hay más gente en casa, usará esa info para decidir si pasar más tarde. La racionalidad depende de lo que ha percibido, no de lo que podría haber percibido.

**Ranas verdes y negras:**

**Medida de rendimiento:** Mover a las ranas de un lado al otro en la menor cantidad de movimientos.

**Conocimiento del medio:** Una rana puede avanzar a una casilla vacía frente a ella, una rana puede saltar a una sola rana, las ranas no pueden retroceder.

**Acciones disponibles:** 

* Avanzar a una casilla vacía.  
* Saltar a una sola rana.

**Secuencia de percepciones:** La posición actual de todas las ranas en el tablero.

**Caníbales y Misioneros:**

**Medida de rendimiento:** Transportar a los tres misioneros y a los tres caníbales del lado inicial del río al lado opuesto, sin que nunca haya más caníbales que misioneros en ninguno de los lados del río, y usando el menor número de cruces posible.

**Conocimiento del medio:** El bote solo puede llevar a una o dos personas a la vez. Siempre debe haber al menos una persona en el bote para cruzar. Los caníbales no pueden superar en número a los misioneros en ninguna orilla.

**Acciones disponibles:**

* Cruzar el río con un misionero.  
* Cruzar el río con un caníbal.  
* Cruzar el río con dos misioneros.  
* Cruzar el río con dos caníbales.  
* Cruzar el río con un misionero y un caníbal.

**Secuencia de percepciones:** El número actual de misioneros y caníbales en cada orilla del río y la posición actual del bote.

**Esposos Celosos:**

**Medida de rendimiento:** Transportar a los tres matrimonios (esposos y esposas) del lado inicial del río al lado opuesto, sin que ninguna esposa se encuentre en presencia de otro hombre sin que su esposo esté presente, y utilizando el menor número de cruces posible.

**Conocimiento del medio:** El bote solo puede llevar a una o dos personas a la vez. Siempre debe haber al menos una persona en el bote para cruzar. Ninguna esposa puede estar en una orilla (o en el bote) en presencia de uno o más hombres a menos que su esposo también esté presente.

**Acciones disponibles:**

* Cruzar el río con un esposo.  
* Cruzar el río con una esposa.  
* Cruzar el río con un matrimonio (esposo y esposa).  
* Cruzar el río con dos esposos.  
* Cruzar el río con dos esposas.

**Secuencia de percepciones:** El número y la identidad de las personas (esposos y esposas) en cada orilla del río y la posición actual del bote.