    def reset_game_after_cash_out(self) -> None:
        """ Resets the game after cashing out """
        self.game_in_progress = False
        self.start_button.setDisabled(True)
        self.gridClass.disable_grid(True)
        self.settingsClass.activate_btns()
        self.settingsClass.reset_bet()
        self.gridClass.reset_buttons()
        self.settingsClass.reset_for_new_game()
        self.settingsClass.disable_cash_out_button()
