import matplotlib.pyplot as plt

# Fungsi untuk membaca data dari file
def read_data(file_path):
    nodes = []
    with open(file_path, 'rt') as f:
        count = 1
        for line in f:
            if count >= 10:
                parts = line.split()
                if len(parts) < 8:
                    continue
                node = {
                    'id': int(parts[0]),
                    'longitude': float(parts[1]),
                    'latitude': float(parts[2]),
                    'name': ' '.join(parts[7:])
                }
                nodes.append(node)
            count += 1
    return nodes

# Fungsi untuk membuat plot node
def plot_nodes(nodes):
    plt.figure(figsize=(10, 10))
    bak_sampah_plotted = False 
    for node in nodes:
        if node['id'] == 0:
            plt.scatter(node['longitude'], node['latitude'], c='k', label='Depot', s=20)  
        else:
            if not bak_sampah_plotted:
                plt.scatter(node['longitude'], node['latitude'], c='steelblue', label='Bak Sampah', s=20)  
                bak_sampah_plotted = True
            else:
                plt.scatter(node['longitude'], node['latitude'], c='steelblue', s=10)  
        plt.text(node['longitude'], node['latitude'] - 0.0005, node['name'], fontsize=6, ha='center', va='top')
    
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Node Visualization')
    plt.legend(loc='lower right')  # Memindahkan legenda ke kanan bawah
    plt.grid(False)  # Menghilangkan garis-garis grid
    plt.show()

if __name__ == '__main__':
    file_path = './koordinat/koordinat-sampah-tinggi.txt'
    nodes = read_data(file_path)
    plot_nodes(nodes)