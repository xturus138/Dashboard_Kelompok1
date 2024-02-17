import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from streamlit_option_menu import option_menu

@st.cache_data
def load_data(url) :
    df = pd.read_csv(url)
    return df

df_data_customer = load_data('https://raw.githubusercontent.com/Handa284/UAS_PDSD_Kelompok_1/main/customers_dataset.csv')
df_data_order_item = load_data('https://raw.githubusercontent.com/Handa284/UAS_PDSD_Kelompok_1/main/order_items_dataset.csv')
df_data_payment = load_data('https://raw.githubusercontent.com/Handa284/UAS_PDSD_Kelompok_1/main/order_payments_dataset.csv')
df_data_order = load_data('https://raw.githubusercontent.com/Handa284/UAS_PDSD_Kelompok_1/main/orders_dataset.csv')
df_data_product_category = load_data('https://raw.githubusercontent.com/Handa284/UAS_PDSD_Kelompok_1/main/product_category_name_translation.csv')
df_data_product = load_data('https://raw.githubusercontent.com/Handa284/UAS_PDSD_Kelompok_1/main/products_dataset.csv')


def Analisis_Perkembangan () :
    df_data_order.dropna(subset=['order_approved_at','order_delivered_carrier_date','order_delivered_customer_date'], axis=0, inplace=True)
    df_data_order.reset_index(drop=True, inplace=True)

    df_data_product.dropna(subset=['product_category_name','product_name_lenght','product_description_lenght','product_photos_qty','product_weight_g','product_length_cm','product_height_cm','product_width_cm'], axis=0, inplace=True)
    df_data_product.reset_index(drop=True, inplace=True)

    data_payment = pd.merge(df_data_payment, df_data_order, on='order_id', how='inner')
    data_payment = data_payment.loc[:, ['order_purchase_timestamp', 'payment_value']]
    if data_payment['order_purchase_timestamp'].dtypes != 'datetime64[ns]':
        data_payment['order_purchase_timestamp'] = pd.to_datetime(data_payment['order_purchase_timestamp'], errors='coerce')

    data_payment['order_purchase_timestamp'] = data_payment['order_purchase_timestamp'].dt.date

    data_payment['year_month'] = pd.to_datetime(data_payment['order_purchase_timestamp']).dt.to_period('M')
    data_payment = data_payment.groupby('year_month')['payment_value'].sum()
    data_payment = pd.DataFrame(data_payment)

    st.write('Nama : Stevanus Ryo Wijaya (10122014)')
    st.write('Pada analisis ini saya ingin memperlihatkan total pendapatan menggunakan matplotlib')
    st.write('Alasan informasi ini dibuat untuk melihat petumbuhan total pendapatan, sehingga perusahaan dapat melihat dengan lebih baik apakah perusahaanya dijalankan dengan baik atau tidak dilihat dari total pendapatannya')

    st.header("Tabel Perkembangan Total Pendapatan")
    st.dataframe(data_payment)
    st.header('Grafik Pertumbuhan Total Pendapatan')

    fig, ax = plt.subplots(figsize=(14, 8))
    ax.plot(data_payment.index.astype(str), data_payment['payment_value'], marker='o')
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Pertumbuhan (%)')
    ax.set_title('Grafik Pertumbuhan Total Pendapatan')


    x_ticks = data_payment.index.astype(str)[::3]
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_ticks, rotation=45) 

    st.pyplot(fig)
    
    with st.expander("Penjelasan Total Pendapatan Tiap Bulan") :
        st.write('Dilihat dari grafik, pertumbuhan pendapatan semakin meningkat awal awal dan puncaknya berada pada bulan november 2017, setelah itu pendapatan menjadi cukup stabil tetapi turun di bulan terakhir. solusi untuk perusahaan adalah dengan meningkatkan aspek aspek seperti layanan, kualitas produk, dan lainnya agar penjulaan dapat kembali meningkat')
    
    
    
    
def Analisis_Kota():
    df_data_order.dropna(subset=['order_approved_at','order_delivered_carrier_date','order_delivered_customer_date'], axis=0, inplace=True)
    df_data_order.reset_index(drop=True, inplace=True)
    
    data_customer = pd.merge(df_data_customer, df_data_order, on='customer_id', how='inner')
    data_customer = pd.merge(data_customer, df_data_order_item, on='order_id', how='inner')

    data_customer['price'] = data_customer['price'] * data_customer['order_item_id']
    data_customer = data_customer.loc[:, ['customer_id', 'customer_city', 'price']]

    grup = data_customer.groupby(['customer_city'])['price'].sum()
    grup1 = grup.nlargest(5)

    st.write('Nama : Raditya Aryabudhi Ramadhan (10122032)')
    st.write('Pada analisis ini saya ingin memperlihatkan kota dengan penjualan tertinggi hingga terendah menggunakan matplotlib')
    st.write('Alasan dibuatnya analisis ini adalah untuk memperlihatkan kota mana yang memiliki penjualan tertinggi hingga terendah, sehingga perusahaan dapat melihat kota mana yang memiliki penjualan tertinggi.')

    st.header("Tabel Kota dari Tertinggi")
    st.dataframe(grup1)
    
    st.header("Diagram Pie 5 Kota Dengan Penjualan Tertinggi")

    fig, ax = plt.subplots()
    expose = [0.1, 0, 0, 0, 0]
    ax.pie(grup1, labels=grup1.index, autopct='%1.1f%%', shadow=True, startangle=50, explode=expose)
    ax.set_title("Top 5 Kota Penjualan dari yang Tertinggi")
    ax.legend(loc="best", bbox_to_anchor=(1.05, 1))

    st.pyplot(fig)

    grup = data_customer.groupby(['customer_city'])['price'].sum()
    grup2 = grup.nsmallest(5)

    st.header("Tabel Kota dari Terendah")
    st.dataframe(grup2)

    st.header("Diagram Pie 5 Kota Dengan Penjualan Terendah")

    fig, ax = plt.subplots()
    expose = [0.1, 0, 0, 0, 0]
    ax.pie(grup2, labels=grup2.index, autopct='%1.1f%%', shadow=True, startangle=50, explode=expose)
    ax.set_title("Top 5 Kota Penjualan dari yang Terendah")
    ax.legend(loc="best", bbox_to_anchor=(1.05, 1))

    st.pyplot(fig)
    
    with st.expander("Penjelasan Analisis Kota") :
        st.write('Kota Sao Paulo memiliki total penjualan yang paling tinggi dan paling signifikan dibandingkan dengan kota-kota lainnya. Sedangkan kota <b>polo petroquimico de triunfo</b> memiliki total penjualan terendah dari kota-kota lainnya.<br> 5 kota dengan penjualan tertinggi tersebut bisa menjadi pusat strategi bisnis dan marketing perusahaan, namun apabila sumber daya yang dimiliki sangat terbatas, kita bisa memusatkannya lagi sehingga hanya 2 kota saja yaitu Sao Paulo dan Rio De Janeiro. Sedangkan untuk 5 kota terendah, ini akan menjadi bahan penelitian bagi perusahaan, mengapa hal demikian bisa terjadi.')
    




def Analisis_Pemesanan():
    df_data_order.dropna(subset=['order_approved_at','order_delivered_carrier_date','order_delivered_customer_date'], axis=0, inplace=True)
    df_data_order.reset_index(drop=True, inplace=True)
    
    data_pemesanan = pd.merge(df_data_payment, df_data_order, on='order_id', how='inner')
    data_pemesanan = data_pemesanan.loc[:, ['order_purchase_timestamp', 'order_id']]
    if data_pemesanan['order_purchase_timestamp'].dtypes != 'datetime64[ns]':
        data_pemesanan['order_purchase_timestamp'] = pd.to_datetime(data_pemesanan['order_purchase_timestamp'], errors='coerce')

    data_pemesanan['order_purchase_timestamp'] = data_pemesanan['order_purchase_timestamp'].dt.date

    data_pemesanan['year_month'] = pd.to_datetime(data_pemesanan['order_purchase_timestamp']).dt.to_period('M')
    data_pemesanan = data_pemesanan.groupby('year_month')['order_id'].count()
    data_pemesanan = pd.DataFrame(data_pemesanan)

    st.write('Nama : Raihan Dafa Alfarizi (10122022)')
    st.write('Pada analisis ini saya ingin menyampaikan tentang pertumbuhan total pemesanan yang terjadi menggunakan matplotlib')
    st.write('Alasan dibuatnya analisis ini adalah untuk mempermudah perusahaan melihat perkembangan pemesanan. Ketika perusahaan dapat dengan mudah melihat perkembangannya maka proses evaluasi bisa diselesaikan dengan cepat.')

    st.header("Tabel Banyaknya Pemesanan Dalam Periode Bulan")
    st.dataframe(data_pemesanan)

    st.header('Grafik Pertumbuhan Total Pemesanan')


    fig, ax = plt.subplots(figsize=(14, 8))
    ax.plot(data_pemesanan.index.astype(str), data_pemesanan.values, marker='o')
    ax.set_title('Grafik Pertumbuhan Total Pemesanan')
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Pertumbuhan (%)')

    x_labels = []
    for i, period in enumerate(data_pemesanan.index):
        if i % 2 == 0:
            x_labels.append(period.strftime('%b %Y'))
        else:
            x_labels.append('')  
    ax.set_xticks(range(len(x_labels)))
    ax.set_xticklabels(x_labels)

    st.pyplot(fig)
    
    with st.expander("Penjelasan Analisis Total Pemesanan") :
        st.write('Pertumbuhan pemesanan meningkat cukup signifikan pada awal-awal hingga puncaknya pada november tahun 2017, tetapi dalam 9 bulan terakhir tidak ada peningkatan yang lebih tinggi daripada peningkatan pada november tahun 2017. Jika hal ini tidak segera diatasi maka ada kemungkinan trend akan mengalami penurunan. Berikut solusi yang dapat dipertimbangkan untuk masalah ini  yaitu membuat promosi musiman dan melakukan program loyalitas pelanggan.')
    
    

def Analisis_Penjualan() :
    data_product = pd.merge(df_data_order_item, df_data_product, on='product_id', how='inner')
    data_product = pd.merge(data_product, df_data_product_category, on='product_category_name', how='inner')

    data_product = data_product.loc[:, ['product_id', 'product_category_name','product_category_name_english']]
    product_counts = data_product['product_category_name_english'].value_counts()

    st.write('Nama : Muhammad Rivaldi Setiawan (10122031)')
    st.write('Pada analisis ini saya ingin meperlihatkan produk mana yang paling diminati menggunakan matplotlib')
    st.write('Alasan dibuatnya analisis ini adalah untuk melihat produk mana yang paling banyak terjual di perusahaan')

    top_5_products = product_counts.nlargest(5)
    st.header("Tabel 5 Produk Dengan Penjualan Terbanyak")
    st.dataframe(top_5_products)

    st.header('Diagram Pie 5 Produk Paling Banyak Diminati')

    fig, ax = plt.subplots()
    expose = [0.1, 0, 0, 0, 0]
    ax.pie(top_5_products, labels=top_5_products.index, autopct='%1.1f%%', shadow=True, explode=expose)
    ax.set_title('5 Produk Paling Banyak Diminati')
    ax.legend(loc="best", bbox_to_anchor=(1.8, 1))

    st.pyplot(fig)
    
    with st.expander("Penjelasan Analisis Penjualan") :
        st.write('Product bed_beth_table menjadi menjadi salah satu kategori yang paling diminati dibandingkan product lainnya sehingga perusahaan dapat mengaturstrategi marketing dari hasil data yang didapatkan')
    
    
def Analisis_Pembayaran(df_data_payment) :
    df_data_payment = df_data_payment.loc[:, ['order_id', 'payment_type']]
    payment_counts = df_data_payment['payment_type'].value_counts()

    st.write('Nama : Andreas Kurnia (10122015)')
    st.write('Pada analisis ini saya ingin menyampaikan  jenis pembayaran terbanyak')
    st.write('Alasan dibuatnya analisis ini adalah untuk melihat penggunaan jenis pembayaraan apa yang peling banyak digunakan oleh pembeli')

    top_payments = payment_counts.nlargest(4)
    st.header("Tabel Dengan 4 Jenis Pembayaran Terbanyak")
    st.dataframe(top_payments)

    st.header('Diagram Pie 4 Jenis Pembayaran Terbanyak digunakan')

    fig, ax = plt.subplots()
    ax.pie(top_payments, labels=top_payments.index, autopct='%1.1f%%', shadow=True)
    ax.set_title('4 Jenis Pembayaran Terbanyak digunakan')
    ax.legend(loc="best", bbox_to_anchor=(1.5, 1))

    st.pyplot(fig)
    
    with st.expander("Penjelasan Analisis Jenis Pembayaran") :
        st.write('Credit card merupakan metode pembayaran yang paling sering digunakan. jika perusahaan ingin meningkatkan pendapatan, perusahaan dapat melakukan promosi atau diskon khusus untuk penggunaan metode pembayaran tertentu. Misalnya, diskon 10% untuk pembayaran dengan voucher. selain memberikan voucher perusahaan dapat meLakukan edukasi kepada pelanggan mengenai keuntungan menggunakan metode pembayaran lainnya. Misalnya, pembayaran dengan boleto bisa lebih aman karena tidak memerlukan detail kartu kredit.')
    
def profile_kelompok() :
    st.markdown("""
                - Kelas : IF-1
                - Kelompok : 1 - Jupyter
                - Anggota :
                    - 10122014 - Stevanus Ryo Wijaya
                    - 10122015 - Andreas Kurnia
                    - 10122022 - Raihan Dafa Alfarizi
                    - 10122031 - Muhammad Rivaldi Setiawan
                    - 10122032 - Raditya Aryabudhi Ramadhan
                """)

with st.sidebar :
    selected = option_menu('Menu',['Profile Kelompok','Analisis Total Pendapatan','Analisis Kota','Analisis Total Pemesanan','Analisis Penjualan','Analisis Jenis Pembayaran'],
    icons =["easel", "graph-up", "graph-up", "graph-up", "graph-up", "graph-up"],
    menu_icon="cast",
    default_index=0)

if (selected == 'Profile Kelompok') :
    st.title('Proyek Analisis Data: Nama dataset')   
    profile_kelompok() 
elif (selected == 'Analisis Total Pendapatan') :
    st.title(f"Analisis Total Pendapatan")
    Analisis_Perkembangan()
elif (selected == 'Analisis Kota') :
    st.title(f"Analisis Kota Penjualan Tertinggi dan Terendah")
    Analisis_Kota()
elif (selected == 'Analisis Total Pemesanan') :
    st.title(f"Analisis Total Pemesanan")
    Analisis_Pemesanan()
elif (selected == 'Analisis Penjualan') :
    st.title(f"Analisis Penjualan")
    Analisis_Penjualan()
elif (selected == 'Analisis Jenis Pembayaran') :
    st.title(f"Analisis Jenis Pembayran")
    Analisis_Pembayaran(df_data_payment)
    