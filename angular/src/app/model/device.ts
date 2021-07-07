export class Device {
  constructor(
    public id: string,
    public on: boolean = false,
    public rgb: Array<number>
  ) {
  }
}
