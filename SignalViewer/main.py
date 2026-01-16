"""Signal Viewer - Interactive visualization of generated signals."""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from pathlib import Path


class FilePicker:
    """Window for selecting .npz file."""
    
    def __init__(self, parent):
        """Initialize file picker dialog."""
        self.parent = parent
        self.selected_file = None
        self.window = None
        self.show_dialog()
    
    def show_dialog(self):
        """Show file selection dialog."""
        current_dir = Path(__file__).parent.parent
        
        self.window = tk.Toplevel(self.parent)
        self.window.title("Select Signal File")
        self.window.geometry("700x300")
        self.window.resizable(False, False)
        
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Title
        title = tk.Label(
            self.window,
            text="Signal Viewer - Select Signal File",
            font=("Arial", 14, "bold"),
            foreground="white",
            background="#333333"
        )
        title.pack(fill=tk.X, padx=20, pady=20)
        
        # Instructions
        instr = tk.Label(
            self.window,
            text="Select a .npz file containing signal data:",
            font=("Arial", 11),
            background="white"
        )
        instr.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        # File selection frame
        file_frame = tk.Frame(self.window, background="white", relief=tk.SUNKEN, borderwidth=1)
        file_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(file_frame, text="File:", font=("Arial", 10, "bold"), background="white").pack(anchor=tk.W, padx=10, pady=(8, 2))
        
        self.file_var = tk.StringVar(value="")
        
        file_entry_frame = tk.Frame(file_frame, background="white")
        file_entry_frame.pack(fill=tk.X, padx=10, pady=(2, 8))
        
        tk.Entry(file_entry_frame, textvariable=self.file_var, font=("Arial", 10), width=60).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        tk.Button(file_entry_frame, text="Browse", command=self.browse_file, width=10, font=("Arial", 10)).pack(side=tk.LEFT)
        
        # Info text
        info = tk.Label(
            self.window,
            text="Supported files: signals_*.npz (e.g., signals_high_resolution_5000.npz)\nThe viewer will display all signals contained in the file.",
            font=("Arial", 9),
            background="white",
            foreground="gray",
            justify=tk.LEFT
        )
        info.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Buttons frame
        button_frame = tk.Frame(self.window, background="white")
        button_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        tk.Button(
            button_frame,
            text="Cancel",
            command=self.on_cancel,
            font=("Arial", 11),
            padx=20,
            pady=8
        ).pack(side=tk.RIGHT, padx=5)
        
        tk.Button(
            button_frame,
            text="Load",
            command=self.on_load,
            font=("Arial", 11),
            foreground="white",
            background="#1a1a1a",
            activeforeground="white",
            activebackground="#000000",
            padx=20,
            pady=8
        ).pack(side=tk.RIGHT, padx=5)
    
    def browse_file(self):
        """Browse for .npz file."""
        path = filedialog.askopenfilename(
            title="Select signal file",
            filetypes=[("NPZ files", "*.npz"), ("All files", "*.*")],
            initialdir=str(Path(__file__).parent.parent)
        )
        if path:
            self.file_var.set(path)
    
    def on_load(self):
        """Handle load button."""
        file_path = self.file_var.get().strip()
        if not file_path:
            messagebox.showwarning("Selection Error", "Please select a file")
            return
        
        if not file_path.endswith('.npz'):
            messagebox.showwarning("Invalid File", "Please select a .npz file")
            return
        
        self.selected_file = file_path
        self.window.destroy()
    
    def on_cancel(self):
        """Handle cancel button."""
        self.selected_file = None
        self.window.destroy()


class SignalViewer:
    """Main application for viewing signals."""
    
    def __init__(self, root):
        """Initialize the Signal Viewer application."""
        self.root = root
        self.root.title("Signal Viewer - Scientific Data Visualization")
        self.root.geometry("1400x800")
        
        # Show file picker
        picker = FilePicker(root)
        root.wait_window(picker.window)
        
        if picker.selected_file is None:
            root.destroy()
            return
        
        # Load the .npz file
        try:
            self.npz_file = picker.selected_file
            print(f"Loading file: {self.npz_file}")
            npz_data = np.load(self.npz_file)
            print(f"NPZ keys: {list(npz_data.files)}")
            
            # Get signals array
            if 'signals' in npz_data:
                self.signals = npz_data['signals']
                print(f"Loaded 'signals' array with shape: {self.signals.shape}")
            elif 'signal' in npz_data:
                self.signals = npz_data['signal']
                print(f"Loaded 'signal' array with shape: {self.signals.shape}")
                if self.signals.ndim == 1:
                    self.signals = np.array([self.signals])
            else:
                # Use first array
                first_key = list(npz_data.files)[0]
                print(f"Using first array: {first_key}")
                self.signals = npz_data[first_key]
                print(f"Array shape: {self.signals.shape}")
                if self.signals.ndim == 1:
                    self.signals = np.array([self.signals])
            
            # Get number of signals
            if self.signals.ndim > 1:
                self.num_signals = self.signals.shape[0]
            else:
                self.num_signals = 1
                self.signals = np.array([self.signals])
            
            print(f"Total signals: {self.num_signals}")
            self.current_index = 0
            self.root.title(f"Signal Viewer - {Path(self.npz_file).name} ({self.num_signals} signals)")
            
        except Exception as e:
            print(f"Error loading file: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")
            root.destroy()
            return
        
        self.setup_ui()
        self.load_signal(0)
    
    def setup_ui(self):
        """Set up the user interface."""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top control panel
        control_frame = ttk.LabelFrame(main_frame, text="Navigation", padding=10)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Signal selector
        selector_frame = ttk.Frame(control_frame)
        selector_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(selector_frame, text="Signal #:").pack(side=tk.LEFT, padx=5)
        self.signal_var = tk.StringVar(value="1")
        self.signal_combo = ttk.Combobox(
            selector_frame, 
            textvariable=self.signal_var, 
            values=[str(i+1) for i in range(self.num_signals)],
            state="readonly",
            width=10
        )
        self.signal_combo.pack(side=tk.LEFT, padx=5)
        self.signal_combo.bind("<<ComboboxSelected>>", self.on_signal_selected)
        
        # Navigation buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="◄ Previous", command=self.prev_signal).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Next ►", command=self.next_signal).pack(side=tk.LEFT, padx=5)
        
        self.index_label = ttk.Label(button_frame, text=f"1 / {self.num_signals}")
        self.index_label.pack(side=tk.LEFT, padx=20)
        
        ttk.Button(button_frame, text="📁 Change File", command=self.change_file).pack(side=tk.RIGHT, padx=5)
        
        # Go to signal frame
        goto_frame = ttk.Frame(control_frame)
        goto_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(goto_frame, text="Go to signal #:").pack(side=tk.LEFT, padx=5)
        self.goto_var = tk.StringVar(value="1")
        goto_entry = tk.Entry(goto_frame, textvariable=self.goto_var, width=8, font=("Arial", 10))
        goto_entry.pack(side=tk.LEFT, padx=5)
        
        btn = tk.Button(
            goto_frame, 
            text="Jump", 
            command=self.goto_signal,
            font=("Arial", 10),
            background="#1a1a1a",
            foreground="white",
            activebackground="#000000",
            activeforeground="white",
            relief=tk.RAISED,
            bd=1
        )
        btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(goto_frame, text=f"(1 - {self.num_signals})", foreground="gray").pack(side=tk.LEFT, padx=5)
        
        # Main content area
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Signal plot
        self.plot_frame = ttk.LabelFrame(content_frame, text="Signal Visualization", padding=5)
        self.plot_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Right panel - Metadata
        self.metadata_frame = ttk.LabelFrame(content_frame, text="Properties", padding=10)
        self.metadata_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        
        # Create scrollable metadata display
        canvas = tk.Canvas(self.metadata_frame, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.metadata_frame, orient=tk.VERTICAL, command=canvas.yview)
        self.metadata_content = ttk.Frame(canvas, padding=5)
        
        self.metadata_content.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.metadata_content, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bottom status bar
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        self.status_label = ttk.Label(status_frame, text="Ready", relief=tk.SUNKEN)
        self.status_label.pack(fill=tk.X)
    
    def load_signal(self, index: int):
        """Load and display a signal by index."""
        if not (0 <= index < self.num_signals):
            return
        
        self.current_index = index
        self.signal_var.set(str(index + 1))
        self.goto_var.set(str(index + 1))
        
        try:
            signal = self.signals[index]
            
            # Update labels
            self.index_label.config(text=f"{index + 1} / {self.num_signals}")
            
            # Plot signal
            self.plot_signal(signal, index)
            
            # Display metadata
            self.display_metadata(index, signal)
            
            self.status_label.config(text=f"Loaded signal #{index + 1}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load signal: {e}")
            self.status_label.config(text=f"Error loading signal")
    
    def plot_signal(self, signal: np.ndarray, index: int):
        """Plot the signal using matplotlib."""
        # Clear previous plot
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        
        if signal is None:
            label = ttk.Label(self.plot_frame, text="Signal data not found", foreground="red")
            label.pack(pady=20)
            return
        
        # Create figure
        fig = Figure(figsize=(8, 5), dpi=100)
        ax = fig.add_subplot(111)
        
        # Generate time axis
        t = np.arange(len(signal))
        
        # Plot signal
        ax.plot(t, signal, linewidth=1.5, color='steelblue', label='Signal')
        ax.set_xlabel('Sample', fontsize=10)
        ax.set_ylabel('Amplitude', fontsize=10)
        ax.set_title(f'Signal #{index + 1} Waveform', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper right')
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def display_metadata(self, index: int, signal: np.ndarray):
        """Display signal properties."""
        # Clear previous metadata
        for widget in self.metadata_content.winfo_children():
            widget.destroy()
        
        # Title
        title = tk.Label(
            self.metadata_content, 
            text=f"Signal #{index + 1}", 
            font=("Arial", 14, "bold"),
            foreground="white",
            background="#333333"
        )
        title.pack(anchor=tk.W, pady=(0, 10), fill=tk.X, padx=5)
        
        # File info
        file_info = tk.Label(
            self.metadata_content,
            text=f"File: {Path(self.npz_file).name}",
            font=("Arial", 9),
            foreground="#00FF00",
            background="#2a2a2a"
        )
        file_info.pack(anchor=tk.W, pady=(0, 10), fill=tk.X, padx=5)
        
        # Separator
        sep = ttk.Separator(self.metadata_content, orient=tk.HORIZONTAL)
        sep.pack(fill=tk.X, pady=5)
        
        # Signal properties
        properties = [
            ("Signal Index", str(index)),
            ("Samples", str(len(signal))),
            ("Min Value", f"{signal.min():.6f}"),
            ("Max Value", f"{signal.max():.6f}"),
            ("Mean", f"{signal.mean():.6f}"),
            ("Std Dev", f"{signal.std():.6f}"),
        ]
        
        for label, value in properties:
            frame = tk.Frame(self.metadata_content, background="#2a2a2a")
            frame.pack(fill=tk.X, pady=4, padx=5)
            
            ttk.Label(frame, text=f"{label}:", font=("Arial", 11, "bold"), width=15).pack(side=tk.LEFT)
            value_label = tk.Label(frame, text=value, font=("Arial", 11), foreground="#00FF00", background="#2a2a2a")
            value_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    def prev_signal(self):
        """Load previous signal."""
        self.load_signal((self.current_index - 1) % self.num_signals)
    
    def next_signal(self):
        """Load next signal."""
        self.load_signal((self.current_index + 1) % self.num_signals)
    
    def on_signal_selected(self, event):
        """Handle signal selection from dropdown."""
        try:
            signal_num = int(self.signal_var.get())
            index = signal_num - 1
            self.load_signal(index)
        except ValueError:
            pass
    
    def goto_signal(self):
        """Jump to a specific signal by number."""
        try:
            signal_num = int(self.goto_var.get())
            index = signal_num - 1
            
            if 0 <= index < self.num_signals:
                self.load_signal(index)
                self.goto_var.set(str(signal_num))
            else:
                messagebox.showwarning(
                    "Invalid Number",
                    f"Please enter a number between 1 and {self.num_signals}"
                )
                self.goto_var.set(str(self.current_index + 1))
        except ValueError:
            messagebox.showwarning(
                "Invalid Input",
                "Please enter a valid number"
            )
            self.goto_var.set(str(self.current_index + 1))
    
    def change_file(self):
        """Change signal file and reload."""
        picker = FilePicker(self.root)
        self.root.wait_window(picker.window)
        
        if picker.selected_file is None:
            return
        
        try:
            self.npz_file = picker.selected_file
            npz_data = np.load(self.npz_file)
            
            # Get signals array
            if 'signals' in npz_data:
                self.signals = npz_data['signals']
            elif 'signal' in npz_data:
                self.signals = npz_data['signal']
                if self.signals.ndim == 1:
                    self.signals = np.array([self.signals])
            else:
                first_key = list(npz_data.files)[0]
                self.signals = npz_data[first_key]
                if self.signals.ndim == 1:
                    self.signals = np.array([self.signals])
            
            if self.signals.ndim > 1:
                self.num_signals = self.signals.shape[0]
            else:
                self.num_signals = 1
                self.signals = np.array([self.signals])
            
            self.root.title(f"Signal Viewer - {Path(self.npz_file).name} ({self.num_signals} signals)")
            
            # Update combobox
            self.signal_combo['values'] = [str(i+1) for i in range(self.num_signals)]
            
            self.current_index = 0
            self.load_signal(0)
            self.status_label.config(text=f"File changed. Loaded {self.num_signals} signals")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to change file: {e}")


def main():
    """Main entry point."""
    root = tk.Tk()
    app = SignalViewer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
