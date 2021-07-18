export class Device {
  constructor(
    public id: string,
    public on: boolean = false,
    public rgba: Array<number>,
    public event? : string
  ) {
  }
}
