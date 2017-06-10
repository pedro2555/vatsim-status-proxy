# vatsim-status-proxy

## Usage Examples

_Notes_ All coordinates are specified as [long,lat] in decimal degrees

Query a connected client by it's callsign

	/clients?where={"callsign":""}

Query connected clients by their current location, given a center coordinate and a radius (in meters)

	/clients?where={"location":{"$near":{"$geometry":{"type":"Point","coordinates":[-7.9398969,37.0178]},"$maxDistance":250000}}}
