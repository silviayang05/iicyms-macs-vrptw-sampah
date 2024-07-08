import matplotlib.pyplot as plt
from multiprocessing import Queue as MPQueue

class VrptwAcoFigure:
    def __init__(self, nodes: list, path_queue: MPQueue):
        self.nodes = nodes
        self.figure = plt.figure(figsize=(10, 10))
        self.figure_ax = self.figure.add_subplot(1, 1, 1)
        self.path_queue = path_queue
        self._depot_color = 'k'
        self._customer_color = 'steelblue'
        self._line_colors = ['red', 'yellow', 'blue', 'green', 'purple', 'orange', 'pink', 'brown', 'gray', 'cyan']

    def _draw_point(self):
        # Menggambar depot
        self.figure_ax.scatter([self.nodes[0].x], [self.nodes[0].y], c=self._depot_color, label='depot', s=40)
        self.figure_ax.text(self.nodes[0].x, self.nodes[0].y - 0.0005, self.nodes[0].name, fontsize=6, ha='center', va='top')

        # Menggambar customer
        for node in self.nodes[1:]:
            self.figure_ax.scatter(node.x, node.y, c=self._customer_color, label='customer', s=20)
            self.figure_ax.text(node.x, node.y - 0.0005, node.name, fontsize=6, ha='center', va='top')
        plt.pause(0.5)

    def run(self):
        # Pertama, gambar semua node
        self._draw_point()
        self.figure.show()

        # Membaca path baru dari antrian dan menggambarnya
        while True:
            try:
                if not self.path_queue.empty():
                    # Ambil path terbaru dari antrian, path lainnya dibuang
                    info = self.path_queue.get()
                    while not self.path_queue.empty():
                        info = self.path_queue.get()

                    # Debug print untuk memeriksa data yang diterima
                    print(f"Received info: {info}")

                    path, distance, used_vehicle_num = info.get_path_info()
                    if path is None:
                        print('[draw figure]: exit')
                        break

                    # Perlu mencatat line yang akan dihapus, tidak bisa langsung dihapus dalam loop pertama,
                    # karena self.figure_ax.lines akan berubah selama loop, menyebabkan beberapa line tidak bisa dihapus
                    remove_obj = []
                    for line in self.figure_ax.lines:
                        if line.get_label() == 'line':
                            remove_obj.append(line)

                    for line in remove_obj:
                        line.remove()  # Menggunakan metode remove dari objek Line2D
                    remove_obj.clear()

                    # Menggambar ulang line
                    self.figure_ax.set_title('travel distance: %0.2f, number of vehicles: %d ' % (distance, used_vehicle_num))
                    self._draw_line(path)
                plt.pause(1)
            except Exception as e:
                print(f"An error occurred: {e}")

    def _draw_line(self, path):
        # Menggambar path berdasarkan vehicle
        vehicle_index = 0
        for i in range(1, len(path)):
            x_list = [self.nodes[path[i - 1]].x, self.nodes[path[i]].x]
            y_list = [self.nodes[path[i - 1]].y, self.nodes[path[i]].y]
            color = self._line_colors[vehicle_index % len(self._line_colors)]  # Pilih warna berdasarkan indeks vehicle
            self.figure_ax.plot(x_list, y_list, color=color, linewidth=1, label='line')
            plt.pause(0.2)
            if path[i] == 0:  # Jika kembali ke depot, ganti warna
                vehicle_index += 1
