import streamlit as st
from itertools import combinations
import time

class Saham:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return f"Saham(name='{self.name}', price={self.price}, quantity={self.quantity})"

def greedy_buy_sahams(saham_list, budget):
    # Sort the saham list by price in ascending order
    saham_list.sort(key=lambda saham: saham.price)

    stocksName = []
    qtyStocks = []
    total_stocks = 0
    total_cost = 0
    startTime = time.perf_counter_ns()
    for saham in saham_list:
        max_quantity_affordable = min(saham.quantity, (budget // saham.price))
        if max_quantity_affordable > 0:
            stocksName.append(saham.name)
            qtyStocks.append(int(max_quantity_affordable))
            total_cost += max_quantity_affordable * saham.price
            total_stocks += int(max_quantity_affordable)
            budget -= max_quantity_affordable * saham.price
        else:
            break

    endTime = time.perf_counter_ns()
    timeTaken = endTime-startTime
    return total_stocks, total_cost, stocksName, qtyStocks, timeTaken

def brute_force_buy_sahams(saham_list, budget):
    max_stocks = 0
    min_cost = float('inf')
    best_combination = []

    startTime = time.perf_counter_ns()
    # Generate all combinations of Saham objects and their possible quantities
    for r in range(1, len(saham_list) + 1):
        for combo in combinations(saham_list, r):
            for quantities in range_combinations([s.quantity for s in combo]):
                total_cost = sum(s.price * q for s, q in zip(combo, quantities))
                total_stocks = sum(quantities)
                
                if total_cost <= budget and total_stocks > max_stocks:
                    max_stocks = total_stocks
                    min_cost = total_cost
                    best_combination = [(s.name, q) for s, q in zip(combo, quantities)]
    
    endTime = time.perf_counter_ns()
    timeTaken = endTime-startTime
    return max_stocks, min_cost, best_combination, timeTaken

def range_combinations(quantity_list):
    # Generate all possible combinations of quantities for given stocks
    if not quantity_list:
        return [[]]
    first, rest = quantity_list[0], quantity_list[1:]
    sub_combinations = range_combinations(rest)
    return [[i] + sub for i in range(first + 1) for sub in sub_combinations]

# Buat tampilan UI dengan Streamlit
st.title("Mengoptimalkan Pembelian Saham-saham Tertentu dengan Budget yang Telah Diatur")
st.header("Masukkan Data Saham")

# Masukkan data saham
sahamName_list = st.text_input("Masukkan nama saham yang ingin dibandingkan (pisahkan dengan koma): ")
sahamPrice_list = st.text_input("Masukkan harga saham yang ingin dibandingkan (pisahkan dengan koma): ")
sahamQty_list = st.text_input("Masukkan qty saham yang ingin dibandingkan (pisahkan dengan koma): ")

# Konversi input menjadi list
sahamName_list = [x.strip() for x in sahamName_list.split(",")]
sahamPrice_list = [float(x) for x in sahamPrice_list.split(",")]
sahamQty_list = [int(x) for x in sahamQty_list.split(",")]

# Buat list saham
saham_list = []
for i in range(len(sahamName_list)):
    saham_list.append(Saham(sahamName_list[i], sahamPrice_list[i], sahamQty_list[i]))

# Masukkan budget
budget = st.number_input("Masukkan budget yang ingin ditentukan untuk berinvestasi: ")

# Jalankan algoritma Greedy dan Brute Force
stocks_bought_greedy, cost_spent_greedy, stocksName_greedy, qtyStocks_greedy, timeTakenGreed = greedy_buy_sahams(saham_list, budget)
stocks_bought_brute, cost_spent_brute, best_combination_brute, timeTakenBrute = brute_force_buy_sahams(saham_list, budget)

# Tampilkan hasil
st.header("Hasil")
st.write("HASIL DARI GREEDY")
st.write(f"Maximum stocks bought: {stocks_bought_greedy}")
st.write(f"Total cost spent: {cost_spent_greedy}")
st.write(f"Saham yg dibeli: {stocksName_greedy, qtyStocks_greedy}")
st.write(f"Waktu eksekusi: {format((timeTakenGreed/1000000000),'.10f')}")
st.write("")
st.write("HASIL DARI BRUTEFORCE")
st.write(f"Maximum stocks bought: {stocks_bought_brute}")
st.write(f"Total cost spent: {cost_spent_brute}")
st.write(f"Saham yg dibeli: {best_combination_brute}")
st.write(f"Waktu eksekusi: {format((timeTakenBrute/1000000000),'.10f')}")