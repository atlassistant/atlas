import io from 'socket.io-client';

/**
 * Represents a facade used to access the backend parsing stuff
 */
export default class WsService {

  /**
   * Instantiate a new Web socket service.
   * 
   * @param {Function} on_ask 
   * @param {Function} on_show 
   * @param {Function} on_terminate 
   * @param {Function} on_work 
   * @param {Function} on_created 
   * @param {Function} on_disconnect 
   */
  constructor(on_ask, on_show, on_terminate, on_work, on_created, on_disconnect) {
    this.socket = io();
    this.socket.on('ask', on_ask);
    this.socket.on('show', on_show);
    this.socket.on('terminate', on_terminate);
    this.socket.on('work', on_work);
    this.socket.on('destroyed', on_disconnect);
    this.socket.on('disconnect', on_disconnect);
    this.socket.on('created', on_created);
  }

  /**
   * Sends a parse request to the backend
   * 
   * @param {string} text 
   */
  parse(text) {
    this.socket.emit('parse', text);
  }

}
